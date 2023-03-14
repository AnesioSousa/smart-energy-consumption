import smartmeter

MESSAGE_TYPE = "HH1024s"  # Regex?

MESSAGE_TYPE_HELLO = 1
MESSAGE_TYPE_DATA = 2
MESSAGE_TYPE_GOODBYE = 3


def main():
    my_meter = smartmeter.SmartMeter('127.0.0.1', 65120)
    my_meter.sendMeasure(('127.0.0.1', 65120),
                         MESSAGE_TYPE_DATA)


main()
