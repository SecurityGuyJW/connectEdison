# Project Title

Establish a socket connection from the intel edison to AWS.

Project shoueld be able to

1.ping the server
2.pubish data to AWS topics
3.subscribe to AWS topics


### areas of intrest

  This is part of the code covers publishing to a topic on AWS, shows main work being done.

	edisonClient.publish(edisonTopic, iphoneMessage + str(loopCount), 1)
  edisonClient.publish(edisonTopic, emailMessage + (str(loopCount) * 2), 1)
  edisonClient.publish(edisonTopic, emailJSONMessage + (str(loopCount) * 3), 1)
  edisonClient.publish(edisonTopic, httpMessage, 1)
  edisonClient.publish(edisonTopic, httpsMessage, 1)

### coding style

Scripting style is used to complete work. Goals of the project do not require an OOP solution.

## Deployment

Script was deployed on AWS cloud 3AUG2017.

## Versioning

This script in its entirety will not be updated.

## Authors

* **Juan A Wagner** - *Initial work* - [SPAWAR](https://www.linkedin.com/in/juanwagner/)

## License

NONE use code as you wish.

## Acknowledgments

* The graybeards that keep it all together.
