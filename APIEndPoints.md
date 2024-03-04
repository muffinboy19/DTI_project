# API EndPoints

A successful response from the server will look like this:

```json
{
  "status": "success",
  "msg": "success message for the developer",
  "data": {
    "data received from server will be here"
  }
}
```

An error response from the server will look like this:

```json
{
  "status": "error",
  "error": "Error message for the developer",
}
```

The following properties of every endpoint will be descibed in this file:

- **Method**: GET | POST | PATCH | DELETE
- **Authorized**: (Authentication is required or not for this route) True | False
- **Request Parameters**: (Requet-Body to be sent along with the request, for POST | PATCH | DELETE methods)
- **Query Parameters**: (Query Parameters available in GET requests to manipulate the response from the server)
- **Response Data**: (The format of data which is expected from the server with a successful response)

> For Authorized routes send the jwt token as bearer token in request header

## User Authentication

### Register

- **URL:** /auth/register
- **Method:** POST
- **Request Body:**
  - **name:** String
  - **password:** String
  - **email:** String
- **Success Status Code:** 200
- **Response Data:**

    ```json
    {
        "msg": "user registered successfully",
        "status": "success",
        "token": "<jwt_token>"
    }
    ```

### Login

- **URL:** /auth/login
- **Method:** POST
- **Request Body:**
  - **email:** String
  - **password:** String
- **Success Status Code:** 200
- **Response Data:**

    ```json
    {
        "msg": "user logged in successfully",
        "status": "success",
        "token": "<jwt_token>"
    }  
    ```

## Camera Routes

### Add Camera

- **URL:** /camera/addCamera
- **Method:** POST
- **Authorized:** True
- **Request Body:**
  - **rtsp:** String
  - **camera_name:** String
- **Success Status Code:** 200
- **Response Data:**

    ```json
     {
        "camera": {
            "_id": "<mongodb_id>",
            "camera_name": "<camera_name>",
            "current_status": "off",
            "recordings": "<empty_array>",
            "rtsp_url": "<rtsp_url>"
        },
        "msg": "camera added successfully",
        "status": "success"
    }
    ```

### Get camera list 

- **URL:** /camera/camera_list        
- **Method:** GET
- **Authorized:** True
- **Success Status Code:** 200
- **Response Data:**

    ```json
    {
        "camera_list": [
            {
                "_id": "<mongodb_id>",
                "camera_name": "<camera_name>",
                "current_status": "<on/off>",
                "recordings": "<array_with_recording_url>",
                "rtsp_url": "<rtsp_url>"
            },
            {
                "_id": "<mongodb_id>",
                "camera_name": "<camera_name>",
                "current_status": "<on/off>",
                "recordings": "<array_with_recording_url",
                "rtsp_url": "<rtsp_url>"
            }
        ],
        "msg": "camera list obtained successfully",
        "status": "success"
    }
    ```

### Delete Camera

- **URL:** /camera/delete_camera      
- **Method:** DELETE
- **Authorized:** True
- **Request Body:**
  - **camera_id:** String (mongodb id)
- **Success Status Code:** 200
- **Response Data:**

    ```json
    {
        "msg": "camera deleted successfully",
        "status": "success"
    }
    ```

### Update Camera Name

- **URL:** /camera/update_camera_name
- **Method:** PATCH
- **Authorized:** True
- - **Request Body:**
  - **camera_id:** String (mongodb id)
  - **new_camera_name:** String
- **Success Status Code:** 200
- **Response Data:**

    ```json
    {
        "msg": "camera name updated successfully",
        "status": "success"
    }
    ```

## Service Routes

### Start Service

- **URL:** /user/start  
- **Method:** POST
- **Authorized:** True
- **Request Body:**
  - **camera_id:** String (mongodb id)
  - **device_token:** String (device token of phone obtained from firebase)
- **Success Status Code:** 200
- **Response Data:**

    ```json
    {
        "status": "success",
        "msg": "testing started successfully"
    }
    ```

### View live Recording

- **URL:** /user/view?id=<camera_id> (mongodb id)
- **Method:** GET
- **Authorized:** True
- **Success Status Code:** 200
- **Response Data:**

    ```json
      "<Continuous jpg images yeilded to form video smooth streaming>"
    ```
  > The response can be viewed using an img tag in html with the src as this route


## Recordings Routes

### Get Recordings

- **URL:** /recording/get_recordings?id=<camera_id> (mongodb id)
- **Method:** GET
- **Authorized:** True
- **Success Status Code:** 200
- **Response Data:**

    ```json
    {
        "msg": "recordings obtained successfully",
        "recordings": [
            {
                "anomaly": "<anomaly_type>",
                "current_time": "<time_when_anomaly_detected>",
                "filename": "<filename>",
                "video_url": "<video_url.avi>"
            },
            {
                "anomaly": "<anomaly_type>",
                "current_time": "<time_when_anomaly_detected>",
                "filename": "<filename>",
                "video_url": "<video_url.avi>"
            }
        ],
        "status": "success"
    }
    ```

### Delete Recording

- **URL:** /recording/delete_recording    
- **Method:** DELETE
- **Authorized:** True
- **Request Body:**
  - **camera_id:** String (mongodb id)
  - **filename:** String 
- **Success Status Code:** 200
- **Response Data:**

    ```json
    {
        "msg": "recording deleted successfully",
        "status": "success"
    }
    ```
