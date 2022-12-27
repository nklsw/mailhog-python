# mailhog-python

A python client for the [Mailhog](https://github.com/mailhog/MailHog) API


## Installation

Install from PyPI 

```
pip install mailhog
```

## Get Started

```python
from mailhog import Mailhog

mailhog = Mailhog() # Defaults to http://localhost:8025

# Get all messages
mailhog.messages()

# Get all messages with start and limit parameters
mailhog.messages(start=0, limit=10)

# Search for messages
mailhog.search('Text contained in the message')

# Search for messages by recipient
mailhog.search('test@test.com', 'To')

# Search for messages by sender
mailhog.search('test@test.com', 'From')

# Delete all messages
mailhog.delete_all()
```

# API
##  mailhog.Mailhog
> Mailhog API client
#### Parameters

* `host` - The host of the Mailhog API, defaults to `localhost`
* `port` - The port of the Mailhog API, defaults to `8025`

### Methods
### `messages(start=0, limit=10)`
> Get all messages

#### Parameters
* `start` - The start index of the messages to return, defaults to `0`
* `limit` - The number of messages to return, defaults to `10`

#### Returns
* `list` - A list of `mailhog.Message` objects

#### Example
```python
from mailhog import Mailhog

mailhog = Mailhog()

messages = mailhog.messages()
```

### `search(query, kind='containing', start=0, limit=10)`
> Search for messages

#### Parameters
* `query` - The query to search for
* `kind` - The kind of search to perform, defaults to `containing`
* `start` - The start index of the messages to return, defaults to `0`
* `limit` - The number of messages to return, defaults to `10`

#### Returns
* `list` - A list of `mailhog.Message` objects

#### Example
```python
from mailhog import Mailhog

mailhog = Mailhog()

messages = mailhog.search('Some Text')
```

### `delete_all()`
> Delete all messages

#### Example
```python
from mailhog import Mailhog

mailhog = Mailhog()

mailhog.delete_all()
```

# Datatypes
##  mailhog.Messages
> A list of `mailhog.Message` objects
#### Attributes
* `total` - The total number of messages
* `start` - The start index of the messages
* `count` - The total number of received messages
* `items` - A list of `mailhog.Message` objects

##  mailhog.Message
> A message from Mailhog
#### Attributes
* `id` - The ID of the message
* `from_` - A mailhog.Path object containing the sender
* `to` - A List of mailhog.Path objects containing the recipients
* `created` - The date the message was created
* `content` - A mailhog.Content object containing the content of the message
* `raw`: - The raw message
* `mime` - A mailhog.MIME object containing the MIME data of the message

#### Methods
### `get_sender()`
> Get the sender of the message

#### Returns
* `str` - The sender of the message

### `get_recipients()`
> Get the recipients of the message

#### Returns
* `list` - A list of recipients

### `get_subject()`
> Get the subject of the message

#### Returns
* `str` - The subject of the message

##  mailhog.Path
> A path object
#### Attributes
* `relays` - A list of relays
* `mailbox` - The mailbox
* `domain` - The domain
* `params` - The parameters

##  mailhog.Content
> The content of a message
#### Attributes
* `headers` - A Dict of headers of the message
* `body` - The body of the message
* `size` - The size of the message
* `mime` - The MIME type of the message


##  mailhog.MIMEBody
> The body of a MIME message
#### Attributes
* `parts` - A list of mailhog.MIMEContent objects


##  mailhog.MIMEContent
> The content of a MIME message
#### Attributes
* `headers` - A Dict of headers of the message
* `body` - The body of the message
* `size` - The size of the message
* `mime` - The MIME type of the message

___

## About the Package

### WIP

This package is still a work in progress. If you find any bugs or have any suggestions, please open an issue on the [GitHub repository](https://github.com/nklsw/mailhog-python)

### Roadmap

- [x] Mailhog API v2 Messages Endpoint
- [x] Mailhog API v2 Search Endpoint
- [ ] Mailhog API v2 Jim Endpoint
- [x] Mailhog API v1 Delete Messages Endpoint
- [ ] Mailhog API v1 Delete Message Endpoint


### Local Development

To install the package locally, run the following commands:

```
git clone
cd mailhog-python

poetry install
```

To run a mailhog instance locally, run the following command:

```
docker-compose up -d
```



To run the tests, run the following command:

```
poetry run pytest
```
