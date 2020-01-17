class Runner:

    """theClass : instance of the target Class e.g. leds as an instance of LedController 
theMethod : Target Method e.g. run(), blink(), wave(), pulse()
namespace : namespace for Class """

    @staticmethod
    def run(theClass,theMethod):
        i = 0
        while Runner.check(theClass,theMethod):
            print(str(i)+" running...")
            getattr(theClass,theMethod)()
            i = i+1
            time.sleep(1)
        return

    @staticmethod
    def start(theClass,theMethod):
        namespace = theClass.name+"_"+theMethod
        afile = open('runner_runtime_'+namespace,'w')
        afile.truncate()
        afile.write('1')
        afile.close()

    @staticmethod
    def stop(theClass,theMethod):
        namespace = theClass.name+"_"+theMethod
        afile = open('runner_runtime_'+namespace,'w')
        afile.truncate()
        afile.write('0')
        afile.close()

    @staticmethod
    def check(theClass,theMethod):
        namespace = theClass.name+"_"+theMethod
        afile = open('runner_runtime_'+namespace,'r')
        line = str(afile.read(1)) == "1"
        #print(line)
        afile.close()
        return line


def dailySchedule2(data):
  timeNow = datetime.now()
  timeNow = timeNow.replace(day=7, hour=1, minute=41)
  timeScheduled = timeNow.replace(hour=int(data['spotlight_starttime_hours']), minute=int(data['spotlight_starttime_minutes']))
  timeScheduledOff = timeScheduled + timedelta(hours=int(data['spotlight_duration_hours'])) + timedelta(minutes=int(data['spotlight_duration_minutes']))
  print(str(timeNow.time())+" \n"+str(timeScheduled.time())+" \n"+str(timeScheduledOff.time()))
  if timeScheduled.time() < timeScheduledOff.time() : 
    if timeNow.time() >= timeScheduled.time() and timeNow.time() <= timeScheduledOff.time() :
      print("Now On")
    else : 
      print("Now Off")
  else :
    if timeNow.time() >= timeScheduled.time() or timeNow.time() <= timeScheduledOff.time() :
      print("Now On")
    else : 
      print("Now Off")
      
udata = { 'spotlight_starttime_hours':14,'spotlight_starttime_minutes':20, 'spotlight_duration_hours':14, 'spotlight_duration_minutes':20 }
dailySchedule2(udata)