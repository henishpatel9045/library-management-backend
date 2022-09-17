# Library Management Backend API

## 🛠 Tools Used
Python, Django, Django-Rest-Framework, drf-nestedrouters, djangorestframework-simplejwt, drf-yasg


## Deployment
   [Go to website](https://library00management.pythonanywhere.com/)

## Documentation Link
   [Go to website](https://library00management.pythonanywhere.com/swagger)

## Run Locally

### With Docker
```bash
  docker-compose build
```
```bash
  docker-compose up
```

### Without Docker

#### Using sqlite as database
GOTO library_management/settings/db_select.py
Change USE_POSTGRES=True -> USE_POSTGRES=False

```bash
  pip install -r requirements.txt
```
```bash
  python manage.py migrate
```
```bash
  python manage.py runserver
```

#### Test API
```bash
  pytest
```


## API Reference
### New User Regesteration and login
```http
  POST /auth/regester/
```
```http
  POST /auth/login
```

### Add new book whole flow

<li>Only Librarien can add,update,delete book.</li>
<ol>
    <li>Get JWT token from /auth/login</li>
    <li>Add JWT token in request headers, Authorization: JWT {YOUR_TOKEN}</li>
    <li>Add new book by post method on /book/</li>
</ol>


### Add new member by librarian flow

<ol>
    <li>Get JWT token from /auth/login</li>
    <li>Add JWT token in request headers, Authorization: JWT {YOUR_TOKEN}</li>
    <li>Add new member by post method on /auth/member/</li>
</ol>


### Borrow book flow

<ol>
    <li>Get JWT token from /auth/login</li>
    <li>Add JWT token in request headers, Authorization: JWT {YOUR_TOKEN}</li>
    <li>Get list of books at GET: /book/</li>
    <li>Borrow book POST: /book/{id}/borrow/</li>
</ol>

### Return book flow

<ol>
    <li>Get JWT token from /auth/login</li>
    <li>Add JWT token in request headers, Authorization: JWT {YOUR_TOKEN}</li>
    <li>Get list of books borrowed at GET: /auth/me/{id}/borrowed</li>
    <li>Generate return approval request by POST: /return/</li>
</ol>

### Approve Return
Only Librarian can approve return request.
<ol>
    <li>Get JWT token from /auth/login</li>
    <li>Add JWT token in request headers, Authorization: JWT {YOUR_TOKEN}</li>
    <li>Get list of return approvals at GET: /return</li>
    <li>Approve return approval request by PUT: /return/{id}</li>
</ol>


### Delete Member by Librarien
<ol>
    <li>Get JWT token from /auth/login</li>
    <li>Add JWT token in request headers, Authorization: JWT {YOUR_TOKEN}</li>
    <li>Get list of members at GET: /auth/member</li>
    <li>Delete member by DELETE: /auth/member/{id}</li>
</ol>



### Update Member
<ol>
    <li>Get JWT token from /auth/login</li>
    <li>Add JWT token in request headers, Authorization: JWT {YOUR_TOKEN}</li>
    <li>Get list of members at GET: /auth/member</li>
    <li>Delete member by PUT: /auth/member/{id}</li>
</ol>

### Update Librarian
Only Librarian can update.
<ol>
    <li>Get JWT token from /auth/login</li>
    <li>Add JWT token in request headers, Authorization: JWT {YOUR_TOKEN}</li>
    <li>Get list of members at GET: /auth/member</li>
    <li>Delete member by PUT: /auth/member/{id}</li>
</ol>


## Feedback

If you have any feedback, please reach out to us at henishpatel9045@gmail.com


## Authors

- [@henishpatel9045](https://www.github.com/henishpatel9045)
