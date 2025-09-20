





# predictive_manufacturing/api/delay_predict.py
import frappe
import os
import pickle
import numpy as np

@frappe.whitelist()
def predict_delay(**kwargs):
    try:
        # Safe numeric conversion with fallback to 0
        def to_int(val): return int(val) if val not in [None, ''] else 0
        def to_float(val): return float(val) if val not in [None, ''] else 0.0

        planned_start_days_from_today = to_int(kwargs.get("planned_start_days_from_today"))
        raw_material_available = to_float(kwargs.get("raw_material_available"))
        machine_availability = to_float(kwargs.get("machine_availability"))
        shift_capacity = to_float(kwargs.get("shift_capacity"))
        workforce_available = to_int(kwargs.get("workforce_available"))
        planned_quantity = to_int(kwargs.get("planned_quantity"))
        workstation = kwargs.get("workstation") or "Unknown"

        # Paths to models
        site_path = frappe.get_site_path("public", "files", "models")
        model_path = os.path.join(site_path, "delay_model.pkl")
        ohe_path = os.path.join(site_path, "workstation_ohe.pkl")
        features_path = os.path.join(site_path, "feature_columns.pkl")

        # Load model, encoder, and feature columns
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        with open(ohe_path, "rb") as f:
            ohe = pickle.load(f)
        with open(features_path, "rb") as f:
            feature_columns = pickle.load(f)

        # Encode workstation safely
        try:
            ws_encoded = ohe.transform([[workstation]])
        except Exception:
            # fallback: zeros if unknown workstation
            ws_encoded = np.zeros((1, ohe.categories_[0].shape[0]))

        # Prepare input
        numeric_features = [
            planned_start_days_from_today,
            raw_material_available,
            machine_availability,
            shift_capacity,
            workforce_available,
            planned_quantity
        ]
        X_input = np.hstack([numeric_features, ws_encoded[0]])

        # Predict
        prob = model.predict_proba([X_input])[0][1] * 100  # as percentage

        # Feature importance
        importance = model.feature_importances_
        top_features_idx = np.argsort(importance)[::-1][:3]
        reasons = [f"{feature_columns[i]}: {importance[i]:.2f}" for i in top_features_idx]

        return {
            "delay_probability": round(prob, 2),
            "predicted_reason": ", ".join(reasons)
        }

    except Exception as e:
        # log error in ERPNext
        frappe.log_error(frappe.get_traceback(), "Predict Delay Error")
        return {
            "delay_probability": 0,
            "predicted_reason": "Error in prediction"
        }



# import frappe
# from .delay_predict import predict_delay

# @frappe.whitelist()
# def predict_all_work_orders():
#     high_risk_count = 0
#     updated_count = 0

#     # Get pending Work Orders
#     work_orders = frappe.get_all("Work Order", filters={"status": ["!=", "Completed"]},
#                                  fields=[
#                                      "name",
#                                      "custom_planned_start_days_from_today",
#                                      "custom_raw_material_available",
#                                      "custom_machine_availability",
#                                      "custom_shift_capacity",
#                                      "custom_workforce_available",
#                                      "custom_planned_quantity",
#                                      "custom_workstation"
#                                  ])
#     for wo in work_orders:
#         result = predict_delay(
#             planned_start_days_from_today=wo.custom_planned_start_days_from_today,
#             raw_material_available=wo.custom_raw_material_available,
#             machine_availability=wo.custom_machine_availability,
#             shift_capacity=wo.custom_shift_capacity,
#             workforce_available=wo.custom_workforce_available,
#             planned_quantity=wo.custom_planned_quantity,
#             workstation=wo.custom_workstation
#         )

#         # Update fields in Work Order
#         frappe.db.set_value(wo.name, "custom_ai_delay_probability_", result.get("delay_probability"))
#         frappe.db.set_value(wo.name, "custom_predicted_delay_reason", result.get("predicted_reason"))

#         # Flag high-risk orders
#         if result.get("delay_probability", 0) > 60:
#             high_risk_count += 1
#             frappe.db.set_value(wo.name, "status", "High Risk")

#         updated_count += 1

#     return {"updated_count": updated_count, "high_risk_count": high_risk_count}