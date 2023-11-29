# secure infrastructure

An infrastructure should be designed to be secure without sacrifice performance and operativity.

## Users and groups

## passwords and environment variables

## docker

## web server

Example managed by nginx

```
	location /kafka-ui {
		auth_basic "Administrator s Area";
		auth_basic_user_file /etc/apache2/.htpasswd; 
        proxy_pass http://kafka-ui:8080;
	}
```

## middleware 

## api token

Example in python flask:

```python
def token_required(f):
  @wraps(f)
  def token_dec(*args, **kwargs):
    token = request.headers.get('token')
    if not token:
      return retDict({"status":"token rejected","message":"Missing Token!"}, 400)
    if token != app.config['SECRET_KEY']:
      return retDict({"status":"token rejected","message":"Invalid Token"}, 401)
    return f(*args, **kwargs)
  return token_dec
```
Example in go gorilla/mux

```golang
func generateJWT() (tokenString string, err error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"iat": time.Now().Unix(),
		"exp": time.Now().Add(time.Hour * 1).Unix()})
	tokenString, err = token.SignedString([]byte("secret"))
	return tokenString, err
}
func authenticateRequest(authHeader string) bool {
	data, err := base64.StdEncoding.DecodeString(authHeader)
	if err != nil {
		fmt.Println("error:", err)
		return false
	}
	userpwd := strings.Split(string(data), ":")
	userpwdmap := userpassword()
	if userpwdmap[userpwd[0]] == userpwd[1] {
		return true
	}
	return false
}
 func authenticateJWT(header http.Header) bool {
	jwtString := header.Get("Authentication")
	if len(jwtString) == 0 {
		return false
	}
	token, err := jwt.Parse(jwtString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"])
		}
		return []byte("secret"), nil
	})
	if err == nil && token.Valid {
		return true
	} else {
		return false
	}
	return false
}
```

## web server

Example in nginx with apache2 password generation

```
	location /secret.html {
			 auth_basic "Administrator s Area";
    		 auth_basic_user_file /etc/apache2/.htpasswd;
	}
```

