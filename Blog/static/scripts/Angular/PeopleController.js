var angularApp = angular.module('MongoApp', []);
angularApp.controller('PeopleController', ['$scope', function ($scope) {
	var self = this;

	self.people = [{Name: "teste", Gender:"sdf", Age:34}];

	function loadPeople() {
	    $.ajax({
	        url: "http://localhost:8080/controllers/People",
	        type: "GET",
	        success: function(data) {
	            console.log(data);
	            self.people = [];
	            $(data).each(function() {
	                self.people.push(this);
	            });
	        }
	    });
	}

	self.init = function(){
		loadPeople();
	}
}]);
