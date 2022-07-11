from PyQt5 import QtGui, QtCore

_emailProvidersPattern = ".+@(gmail\\.com|outlook\\.(com|it)|hotmail\\.com|yahoo\\.(com|it)|tim\\.it|alice\\.it|libero\\.it|aruba\\.(com|it))"

class GUIUtils:


	validators = {
		'soloLettere' : QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[a-zA-Z'àèòìù ]+")),
		'soloNumeri' : QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9]+")),
		'email' : QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(_emailProvidersPattern)),
		'cellulare' : QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9]{10,10}")),
		'IBAN' : QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9]{27,27}")), # 27 numeri
		'numeroCarta' : QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9]{13,16}")),
		'password' : QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]{8,}$")) # 8 o più caratteri, almeno una maiuscola, una minuscola e un numero
	}
	