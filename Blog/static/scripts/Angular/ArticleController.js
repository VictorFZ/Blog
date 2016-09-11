var angularApp = angular.module('MongoApp', []);

angularApp.controller('ArticleController', function ($scope, articleFactory) {
    var self = this;

    self.articles = [];

    function loadArticles() {
        self.articles = articleFactory.getArticles(function (response) {
            self.articles = response;
        });
    }

    function loadLoggedUser() {
        self.articles = articleFactory.getArticles(function (response) {
            self.articles = response;
        });
    }

    self.init = function () {
        loadArticles();
    }
});

