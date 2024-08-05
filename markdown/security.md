# secure infrastructure

An infrastructure should be designed to be secure without sacrifice performance and operativity.

# types of data breaches

## Personally Identifiable Information

Personally identifiable information (PII) is any kind of data that can be linked back to an identifiable person. This personal data can include driver’s licenses, dates of birth, social security number, email addresses, phone numbers, credit card numbers, or passwords that are tied to a person’s name, username, or other factors that identify them.
Financial Information

## Financial information

especially when associated with personal information, is especially vulnerable to data breaches. Any financial information gained in a data breach can be used to commit fraud or identity theft, where a bad actor can make unauthorized purchases or reports in someone else’s name.
Health Information

## health information

It may sound strange that health information is often stolen and compromised. However, healthcare remains the most expensive industry in terms of data breaches for 12 years running. The cost of a data breach in this industry averaged $10.10 million in 2022, with the financial industry at a distant second incurring $5.97 million in costs on average. Similarly to financial information, health information can include extremely sensitive PII such as social security numbers, which can be used to commit identity theft. In financial breaches, sometimes only one or two pieces of important information can be revealed. With health information, there is often a wider array of PII available in one place.
Intellectual Property

## intellectual property

If an organization has valuable intellectual property, this may also be the motivation for a data breach. Trade secrets, in-process patents, or other confidential information may be highly valuable if sold to the right buyer. Malicious insiders may know someone who wants this information – just over 10% of all data breaches are attributed to actions from people on the inside.
Competitive Intelligence

## competitive intelligence

Similarly, competition information may be of interest to the right audience. Whether a business has collected information about their competitors, or a competitor is interested in uncovering more about the pricing or marketing strategies of a business, certain information can be used to gain a competitive advantage.
Legal Information

## legal information

Legal documents, such as agreements and contracts, may be valuable, especially for the sensitive data they can contain. Data that is found in legal information can be used to commit fraud, similar to financial and health information.
IT Security Information

## IT security

Just like PII can open the floodgates and uncover more sensitive information as criminals connect the dots, IT security information can play the same role in the systems of an organization. Uncovering passwords or other important credentials can serve as an open door, sometimes allowing access to entire systems.

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

