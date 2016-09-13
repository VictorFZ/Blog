var angularApp = angular.module('MongoApp', []);

angularApp.controller('ArticleController', function ($scope, articleFactory) {
    var self = this;

    self.loggedUser = null;
    self.loginEmailInput = "";
    self.loginPasswordInput = "";
    self.loginError = false;

    self.signinError = false;
    self.signinMessage = "";

    self.signinEmailInput = "";
    self.signinPasswordInput = "";
    self.signinConfirmPasswordInput = "";
    self.signinNameInput = "";

    self.articles = [];

    function loadArticles() {
        articleFactory.getArticles(function (response) {
            self.articles = response;
        }, function () { });
    }

    function loadLoggedUser() {
        articleFactory.getLoggedUser(function (response) {
            if (response != "") {
                self.loggedUser = response;
            } else {
                self.loggedUser = null;
            }
        }, function () { });
    }

    function siginError(error, message) {
        self.signinError = error;
        if (!error) {
            self.signinMessage = "";
        } else {
            self.signinMessage = message;
        }
    }

    self.init = function () {
        loadArticles();
        loadLoggedUser();
    }

    self.logInModal = function () {
        $("#loginModal").modal({
            backdrop: 'static',
            keyboard: false
        }).modal("show");
    }

    self.signInModal = function () {
        $("#signinModal").modal({
            backdrop: 'static',
            keyboard: false
        }).modal("show");
    }

    self.login = function () {
        self.loginError = false;
        var loginInfo = {
            email: self.loginEmailInput,
            password: self.loginPasswordInput
        }

        articleFactory.loginUser(loginInfo, function (response) {
            if (response == null || response == "") {
                self.loginError = true;
            } else {
                self.loggedUser = response;
                $("#loginModal").modal("hide");
            }

        }, function () { });
    }

    self.logout = function () {
        articleFactory.logoutUser(function (response) {
            loadLoggedUser();
        }, function() {
            loadLoggedUser();
        });
    }

    self.signin = function() {
        self.signinError = false;

        if (self.signinPasswordInput != self.signinConfirmPasswordInput) {
            siginError(true, "Password and Password Confirmation do not match");
        }

        var signinInfo = {
            name: self.signinNameInput,
            email: self.signinEmailInput,
            password: self.signinPasswordInput
        }

        articleFactory.signinUser(signinInfo, function (response) {
            self.signinError = !response.success;
            if (response.success) {
                $("#signinModal").modal("hide");
                self.loginEmailInput = self.signinEmailInput;
                self.loginPasswordInput = self.signinPasswordInput;
                self.login();
            }
        }, function () { });
    }
});

