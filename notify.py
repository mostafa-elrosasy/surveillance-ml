from pyfcm import FCMNotification

# push_service = FCMNotification(api_key="AAAAc75TZlc:APA91bGURojYU5Bbenzg8HDAgGdMxjbRs-0wm7MfRBebSHBtAaemCUKKOGUodQuE9u_wQbsU9arVdECzUaQN4S_rtTRF4GQPEn74EulU_DNMpi7_cxDAjHVq4vsSVS1Jw_6JLy7WK7im")
push_service = FCMNotification(api_key="e1sEE9dsRSGU5AVJhyPpzw:APA91bGw1prTqq_4WwVofpVfgdN3yB_PM-qV3u52GLX0rQbNy_O0I-OZD4B3MDCq6lZCcflwDDZJygtQEn_GDkGb6ds-Cs6gdNH0kLJmxVz_SXdNrhQjwaCRMDDI_PG90QEHb82o73ue")



def send_notification(message_body, device_id = 0):



    registration_id = "f1l6ZxxbTUWLGwLWM72m3x:APA91bF4vyPfvGAIxpJGc4wgyYYgkLcQ1kfJQRm5w_uKDAe4zKklN5VjNNDFElUTytEj2H8CQZa4O5gDpsz9bGA2GxFxaueE_ow7d_hveXgj1bmDH58sf0NTQix4KSu8RlJ7XJwp8IrA"

    message_title = "Danger!"


    result = push_service.notify_single_device(
        registration_id=registration_id, message_title=message_title,
        message_body=message_body
    )

    # Send to multiple devices by passing a list of ids.

    #registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]



    print(result)



# send_notification("hey")