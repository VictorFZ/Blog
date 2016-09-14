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
    self.selectedArticleOid = "";

    self.createArticleNameInput = "";
    self.createArticleTextInput = "";
    self.createArticleTagsInput = "";
    self.createArticleCategoriesInput = "";
    self.createArticleSlugInput = "";

    self.createArticleError = false;
    self.createArticleMessage = "";

    function bindTooltips() {
        $(".tooltip-item").tooltip('destroy');
        $(".tooltip-item").tooltip();
    }

    function showModal(id) {
        $("#" + id).modal({
            backdrop: 'static',
            keyboard: false
        }).modal("show");
    }

    function hideModal(id) {
        $("#" + id).modal("hide");
    }

    function loadArticles() {
        articleFactory.getArticles(function (response) {
            self.articles = response;
            setTimeout(bindTooltips, 100);
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
        showModal("loginModal");
    }

    self.signInModal = function () {
        showModal("signinModal");
    }

    self.deleteArticleModal = function(oid) {
        showModal("deleteArticleModal");
        self.selectedArticleOid = oid;
    }

    self.createArticleModal = function() {
        showModal("createArticleModal");
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
            } else {
                self.signinMessage = response.message;
            }
        }, function () { });
    }

    self.deleteArticle = function() {
        articleFactory.deleteArticle(self.selectedArticleOid, function (response) {
            self.articles = _.filter(self.articles, function(article) {
                return article.oid != self.selectedArticleOid;
            });
            self.selectedArticleOid = "";
            hideModal("deleteArticleModal");
        }, function () {
            self.selectedArticleOid = "";
            hideModal("deleteArticleModal");
        });
    }

    self.createArticle = function() {
        var article = {};

        article.name = self.createArticleNameInput;
        article.slug = self.createArticleSlugInput;
        article.text = self.createArticleTextInput;
        article.tags = _.map(self.createArticleTagsInput.split(","), function (tag) { return { value: tag } });
        article.categories = _.map(self.createArticleCategoriesInput.split(","), function (cat) { return { value: cat } });

        articleFactory.createArticle(article, function (response) {
            self.createArticleError = !response.success;
            if (response.success) {
                $("#createArticleModal").modal("hide");
                loadArticles();
            } else {
                self.createArticleMessage = response.message;
            }

        }, function () {
            //Show message
        });
    }
});

