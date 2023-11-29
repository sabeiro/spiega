---
title: "Middleware"
author: Giovanni Marelli
date: 2019-07-02
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# middleware

The middleware is here used to handle requests from clients and perform actions on the services and data stored in the cluster.

## authentification

Here is a series of examples of [middleware authentification](https://github.com/sabeiro/sawmill/blob/master/go_ingest/auth.go) in golang

password

```golang
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
```

token

```golang
func generateJWT() (tokenString string, err error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"iat": time.Now().Unix(),
		"exp": time.Now().Add(time.Hour * 1).Unix()})
	tokenString, err = token.SignedString([]byte("secret"))
	return tokenString, err
}
```


## database interface

A simple golang [database extractor](https://github.com/sabeiro/sawmill/blob/master/go_ingest/model.go)

```golang
func (p *queryD) getEntry(db *sql.DB) ([]map[string]interface{}, error)  {
  list := make([]map[string]interface{}, 0)
  queryS := "SELECT " + p.Action + " FROM " + p.Table + " " + p.Filter + ";"
  //   rows, err := db.Query("select 1; select 2") // injest test
  //   fmt.Println(rows)  
  rows, err := db.Query(queryS)
  if err != nil {
    return list, fmt.Errorf("Failed selecting from table: %v", err)
  }
  cols, _ := rows.Columns()
  defer rows.Close()
	for rows.Next() {
    vals := make([]interface{}, len(cols))
    for i, _ := range cols {
        var s string
        vals[i] = &s
    }
    err = rows.Scan(vals...)
    if err != nil {
      return list, fmt.Errorf("Failed selecting from table: %v", err)
    }
    m := make(map[string]interface{})
    for i, val := range vals {m[cols[i]] = val}
    list = append(list, m)
	}
  return list, nil
}
```

## messaging interface

Here is a [python flask/fastapi](https://github.com/sabeiro/sawmill/blob/master/live_py/flask_live.py) middleware to produce and consume messages from kafka

```python
def get_producer():
  return KafkaProducer(bootstrap_servers=[KAFKA_SERVER],api_version=(0,11,15)
                       ,value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def get_consumer():
  return KafkaConsumer(bootstrap_servers=[KAFKA_SERVER],auto_offset_reset='latest'
                       ,consumer_timeout_ms=1000,group_id=GROUP_ID,api_version=(0,11,15)
                       ,fetch_max_bytes=50*1024*1024
                       ,value_deserializer=lambda v: json.loads(v.decode('ascii'))
                       #,key_deserializer=lambda v: json.loads(v.decode('ascii'))
                       ,enable_auto_commit=False,auto_commit_interval_ms=1000)
...
```
