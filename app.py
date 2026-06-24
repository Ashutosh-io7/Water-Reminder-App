from flask import Flask , render_template , jsonify , request 
from plyer import notification 
import logging 

app = Flask(__name__) 

# Configure Logging 
logging.basicConfig(level = logging.INFO , format = '%(asctime)s - %(message)s') 

# Simple In-Memory Database to track stats for the session 
water_log = {
    'total_glass_count' : 0,
    'target_glasses' : 8
}

@app.route('/') 
def home () :
    return render_template('index.html' , log = water_log) 


@app.route('/trigger-notification' , methods = ['POST']) 

def trigger_notification () : 
    """ Trigger a Desktop Notification from the Browser Timer """ 

    try : 
        notification.notify(
            title = '💧 Hydration Time !',
            message = 'Time to Drink a Glass of Water and Stay Healthy !', 
            app_name = 'Hydration App', 
            timeout = 10
        ) 
        logging.info('Desktop Notification Sent.') 

        return jsonify({'status' : 'success' , 'message' : 'Notification sent!'}) 
    
    except Exception as e : 
        logging.error(f'Failed to send Notification : {e}') 
        return jsonify({'status' : 'error' , 'message' : str(e)}) , 500 
    

@app.route('/log-water' , methods = ['POST']) 

def log_water () : 
    """ Log a Glass of Water Drunk """ 
    water_log['total_glass_count'] += 1 
    logging.info(f'Water Logged! Total Today : {water_log["total_glass_count"]} glasses.')

    return jsonify({
        'status' : 'success',
        'current_count' : water_log['total_glass_count'],
        'target' : water_log['target_glasses'] 
    }) 

if __name__ == '__main__' : 
    app.run(debug = True) 