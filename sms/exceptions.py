class SmsException(Exception):
    resultcode = -1

class NoUsernameException(SmsException):
    resultcode = 20

class NoPasswordException(SmsException):
    resultcode = 21

class InvalidOriginatorException(SmsException):
    resultcode = 22

class RecipientMissingException(SmsException):
    resultcode = 23

class MessageMissingException(SmsException):
    resultcode = 24

class InvalidRecipientException(SmsException):
    resultcode = 25

class InvalidOriginatorException(SmsException):
    resultcode = 26

class InvalidMessageException(SmsException):
    resultcode = 27

class ParameterException(SmsException):
    resultcode = 29

class AuthenticationException(SmsException):
    resultcode = 30

class InsufficientCreditsException(SmsException):
    resultcode = 31

class GatewayUnreachableException(SmsException):
    resultcode = 98

class UnknownException(SmsException):
    resultcode = 99

by_code = dict([(i.resultcode, i) for i in [ NoUsernameException, NoPasswordException, InvalidOriginatorException, RecipientMissingException, MessageMissingException, InvalidRecipientException, InvalidOriginatorException, InvalidMessageException, ParameterException, AuthenticationException, InsufficientCreditsException, GatewayUnreachableException, UnknownException ]])
