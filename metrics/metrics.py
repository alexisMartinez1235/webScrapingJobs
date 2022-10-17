from telegraf.client import TelegrafClient
import time
import random
import functools

client = TelegrafClient(host='telegraf', port=8094)

def sendTimeResponseFunction(func):
  @functools.wraps(func)
  def wrapper(self, *args): #, **kwargs):
    print("Monitoring {}".format(func.__name__))
    start = time.time()
    val = func(self, *args) # , **kwargs)
    finish = time.time()
    response_time = finish - start
    client.metric('metrics',  {
      'response_time': response_time,
      'function_name': func.__name__,
    })

    return val
  return wrapper

  
if __name__ == "__main__":
  i=0
  while True:
    time.sleep(4)
    print(i)
    # Records a single value with no tags
    client.metric('some_metric', 123 + (random.randrange(0, 2) - 1) * 10)
    client.metric('json_example', {
      # add time and hostname automatically
      "message": "hello world!"
    })
    i+=1