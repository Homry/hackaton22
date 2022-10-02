# Requests Api

## First you need to sing up or sing ip
### For sing up
```
credentials =   {
                    'email': email,
                    'password': password,
                    'name': name
                }
return fetch(`http://127.0.0.1:5000/user/singup`, {
        method: "POST",
        body: JSON.stringify(credentials),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(function(response) {
        return response.json();
    })
    
    
```
### For sing in

```
credentials =   {
                    'email': email,
                    'password': password
                }
return fetch(`http://127.0.0.1:5000/user/loggin`, {
        method: "POST",
        body: JSON.stringify(credentials),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(function(response) {
        return response.json();
    })

```

In response you get your profile information

## TEST RUN
For test you can use ```/convert_image (POST)``` request
```
return fetch(`http://127.0.0.1:5000/convert_image`, {
        method: "POST",
        body: JSON.stringify(image),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(function(response) {
        return response.json();
    })
```
```image``` - image from your camera with face
response value can be ```byte object``` if face detected, of ```None``` if face doesn`t detect

## Prepare gif
For creating gif you need to use ```/convert_image/<token> (POST)``` as many times as you want to be frames in the gif
```token``` - your ```_id``` from auth

With ```/save_gif/<token> (GET)``` - create gif in server

## Download gif
```/get_gifs/<token>  (GET)``` - return links to all your already created gif files


