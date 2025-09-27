
# Library App Management System API

This is the API of Library App Management System


## Run Locally

Clone the project

```bash
  git clone https://github.com/rikhoari01/libraryapp-fastapi-react.git
```

Go to the project directory

```bash
  cd libraryapp-fastapi-react
```

Go to the project api directory

```bash
  cd library-api
```

Install api depedencies

```bash
  pip install -r requirements.txt
```

Create api env file
```bash
  cp .env.example .env
```

Run api
```bash
  python src/main.py
```



## API Reference

#### API Documentation

```http
  GET /docs
```

### Basic Auth

| Parameter     | Type     | Description                        |
| :--------     | :------- | :--------------------------------  |
| `username`    | `string` | Required for all api endpoint      |
| `password`    | `string` | Required for all api endpoint      |

#### Get books

```http
  GET /api/{API VERSION}/books
```

#### Create book

```http
  POST /api/{API VERSION}/books
```

| Parameter     | Type     | Description                        |
| :--------     | :------- | :--------------------------------  |
| `isbn`        | `string` | isbn of the book                   |
| `title`       | `string` | isbn of the book                   |
| `stock`       | `number` | stock of the book                  |

#### Get book detail by id

```http
  GET /api/{API VERSION}/books/{id}
```

| Parameter     | Type     | Description                        |
| :--------     | :------- | :--------------------------------  |
| `id`          | `number` | id of the book                     |

#### Get book detail by isbn

```http
  GET /api/{API VERSION}/books/isbn/{isbn}
```

| Parameter     | Type     | Description                        |
| :--------     | :------- | :--------------------------------  |
| `isbn`        | `string` | isbn of the book                   |

#### Update book detail

```http
  PUT /api/{API VERSION}/books/{id}
```

| Parameter     | Type     | Description                        |
| :--------     | :------- | :--------------------------------  |
| `id`          | `number` | id of the book                     |
| `isbn`        | `string` | isbn of the book                   |
| `title`       | `string` | isbn of the book                   |
| `stock`       | `number` | stock of the book                  |

#### Delete book

```http
  GET /api/{API VERSION}/books/{id}
```

| Parameter     | Type     | Description                        |
| :--------     | :------- | :--------------------------------  |
| `id`          | `number` | id of the book                     |



#### Get members

```http
  GET /api/{API VERSION}/members
```

#### Create member

```http
  POST /api/{API VERSION}/members
```

| Parameter         | Type     | Description                        |
| :--------         | :------- | :--------------------------------  |
| `id_card_number`  | `string` | id card number of the member       |
| `name`            | `string` | name of the member                 |
| `email`           | `string` | email of the member                |

#### Get member detail by id

```http
  GET /api/{API VERSION}/members/{id}
```

| Parameter     | Type     | Description                        |
| :--------     | :------- | :--------------------------------  |
| `id`          | `number` | id of the member                   |

#### Get member detail by id card

```http
  GET /api/{API VERSION}/members/id-card{isbn}
```

| Parameter         | Type     | Description                        |
| :--------         | :------- | :--------------------------------  |
| `id_card_number`  | `string` | id card number of the member       |


#### Update member detail

```http
  PUT /api/{API VERSION}/members/{id}
```

| Parameter         | Type     | Description                        |
| :--------         | :------- | :--------------------------------  |
| `id`              | `number` | id of the member                   |
| `id_card_number`  | `string` | id card number of the member       |
| `name`            | `string` | name of the member                 |
| `email`           | `string` | email of the member                |


#### Delete member

```http
  DELETE /api/{API VERSION}/members/{id}
```

| Parameter     | Type     | Description                        |
| :--------     | :------- | :--------------------------------  |
| `id`          | `number` | id of the member                   |

#### Get member loan histories

```http
  GET /api/{API VERSION}/members/{id}/loan-history
```

| Parameter     | Type     | Description                        |
| :--------     | :------- | :--------------------------------  |
| `id`          | `number` | id of the member                   |



#### Get loans

```http
  GET /api/{API VERSION}/loans
```

#### Create loans

```http
  POST /api/{API VERSION}/loans
```

| Parameter         | Type     | Description                        |
| :--------         | :------- | :--------------------------------  |
| `member_id`       | `number` | id of the member                   |
| `book_id`         | `number` | id of the book                     |
| `return_deadline` | `date` | book return deadline                 |

#### Get loan detail by id

```http
  GET /api/{API VERSION}/loans/{id}
```

| Parameter     | Type     | Description                        |
| :--------     | :------- | :--------------------------------  |
| `id`          | `number` | id of the loan                     |

#### Get active loans

```http
  GET /api/{API VERSION}/loans/active
```

#### Get overdue loans

```http
  GET /api/{API VERSION}/loans/overdue
```

#### Return book

```http
  PUT /api/{API VERSION}/loans/{id}/return
```

| Parameter     | Type     | Description                        |
| :--------     | :------- | :--------------------------------  |
| `id`          | `number` | id of the loan                     |

