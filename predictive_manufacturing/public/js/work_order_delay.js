frappe.ui.form.on("Work Order", {
    refresh: function(frm) {
        frm.add_custom_button("AI Delay Prediction", function() {

            frappe.call({
                method: "predictive_manufacturing.api.delay_predict.predict_delay",
                args: {
                    planned_start_days_from_today: frm.doc.custom_planned_start_days_from_today,
                    raw_material_available: frm.doc.custom_raw_material_available,
                    machine_availability: frm.doc.custom_machine_availability,
                    shift_capacity: frm.doc.custom_shift_capacity,
                    workforce_available: frm.doc.custom_workforce_available,
                    planned_quantity: frm.doc.custom_planned_quantity,
                    workstation: frm.doc.custom_workstation
                },
                callback: function(r) {
                    if (r.message) {
                        let prob = parseFloat(r.message.delay_probability) || 0;  // ensure number
                        let reason = r.message.predicted_reason || "Not available";

                        // Update fields
                        frm.set_value("custom_ai_delay_probability_", prob);
                        frm.set_value("custom_predicted_delay_reason", reason);
                        // frm.save()
                        frm.refresh_field("custom_ai_delay_probability_");
                        frm.refresh_field("custom_predicted_delay_reason");

                        // Color-coded popup
                        let color = prob < 30 ? "green" : prob < 70 ? "orange" : "red";
                        frappe.msgprint({
                            title: "AI Delay Prediction",
                            indicator: color,
                            message: `Probability: <b style="color:${color}">${prob.toFixed(2)}%</b><br>
                                      Reason: ${reason}`
                        });

                        // Automatically flag high-risk orders
                        let highRiskThreshold = 60;
                        if (prob >= highRiskThreshold) {
                            frm.set_value("status", "High Risk"); // flag status
                            frm.set_df_property("custom_ai_delay_probability_", "description",
                                `<span style="color:red;font-weight:bold">High Risk!</span>`); // show tag
                        } 


                        else {
                            if (frm.doc.status === "High Risk") {
                                frm.set_value("status", "Not Started");  // reset if previously flagged
                            }
                            frm.set_df_property("custom_ai_delay_probability_", "description", "");
                        }

                        //  else {
                        //     // reset if previously flagged
                        //     // if (frm.doc.status === "Low Risk") {
                        //         frm.set_value("status", "Low Risk");
                            
                        //     frm.set_df_property("custom_ai_delay_probability_", "description", 
                        //         `<span style="color:green;font-weight:bold">Low Risk!</span>`);
                        // }
                    }
                }
            });
        });
    },


 custom_ai_delay_probability_: function(frm) {
    let prob = frm.doc.custom_ai_delay_probability_;

    if (prob !== undefined && prob !== null) {
        // ✅ Risk Color Logic
        let color = prob < 30 ? "green" : prob < 70 ? "orange" : "red";

        // ✅ Show message
        frappe.msgprint({
            title: "AI Delay Prediction",
            indicator: color,
            message: `Probability: <b style="color:${color}">${prob.toFixed(2)}%</b>`
        });

        // ✅ Risk Level Logic
        if (prob >= 70) {
            frm.set_value("custom_risk_status", "High Risk");
        } 
        else {
            frm.set_value("custom_risk_status", "Low Risk");
        }

        // ✅ Auto-flag high risk
        if (prob >= 70) {
            frm.set_value("status", "High Risk");
            frm.set_df_property("custom_ai_delay_probability_", "description",
                `<span style="color:red;font-weight:bold">⚠ High Risk!</span>`);
        } else {
            frm.set_df_property("custom_ai_delay_probability_", "description", "");
        }
    }
}



});





// frappe.ui.form.on("Work Order", {
//     refresh: function(frm) {
//         frm.add_custom_button("AI Delay Prediction", function() {

//             frappe.call({
//                 method: "predictive_manufacturing.api.delay_predict.predict_delay",
//                 args: {
//                     planned_start_days_from_today: frm.doc.custom_planned_start_days_from_today,
//                     raw_material_available: frm.doc.custom_raw_material_available,
//                     machine_availability: frm.doc.custom_machine_availability,
//                     shift_capacity: frm.doc.custom_shift_capacity,
//                     workforce_available: frm.doc.custom_workforce_available,
//                     planned_quantity: frm.doc.custom_planned_quantity,
//                     workstation: frm.doc.custom_workstation
//                 },
//                 callback: function(r) {
//                     if (r.message) {
//                         let probability = parseFloat(r.message.delay_probability) || 0;
//                         let reason = r.message.predicted_reason || "Not available";

//                         frm.set_value("custom_ai_delay_probability_", probability);
//                         frm.set_value("custom_predicted_delay_reason", reason);
//                         frm.refresh_field("custom_ai_delay_probability_");
//                         frm.refresh_field("custom_predicted_delay_reason");



// let prob = parseFloat(r.message.delay_probability) || 0;  // ensure number
// let color = prob < 30 ? "green" : prob < 70 ? "orange" : "red";

// frappe.msgprint({
//     title: "AI Delay Prediction",
//     indicator: color,
//     message: `Probability: <b style="color:${color}">${prob.toFixed(2)}%</b><br>
//               Reason: ${r.message.predicted_reason || "Not available"}`
// });



//                     }
//                 }
//             });
//         });
//     }
// });
