def check_for_booking_trigger(user_input):
    """ Check if the user input contains phrases indicating they want to book an appointment. """
    appointment_triggers = [
        "book an appointment", "schedule a meeting", 
        "appointment please", "book appointment", 
        "schedule appointment", "make an appointment"
    ]
    return any(trigger.lower() in user_input.lower() for trigger in appointment_triggers)
