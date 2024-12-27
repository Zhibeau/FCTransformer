import logging
import azure.functions as func
from generate_pictures import generate_pictures
from generate_videos_static import generate_videos_static
from combine_videos import combine_videos
from upload_video import upload_video
import datetime
import logging
import azure.functions as func

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 17 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
@app.route("avideo") 
def everyday_timer(myTimer: func.TimerRequest) -> None:
    generate_pictures()
    generate_videos_static()
    combine_videos()
    upload_video()