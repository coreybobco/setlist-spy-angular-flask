'use strict';

/**
 * @ngdoc function
 * @name setlistspyApp.controller:SetlistSpyCtrl
 * @description
 * # SEtlistSpyCtrl
 * Controller of the setlistspyApp
 */
angular.module('setlistspyApp')
  .controller('SetlistSpyCtrl', function ($scope, $http) ***REMOVED***
    $scope.tracks = [];
    $scope.page = 0;
    $scope.image = "images/setlistspy_logo.jpg";
    $scope.loading = false;
    $scope.setlistSearch = function() ***REMOVED***
      var search_term = JSON.stringify(document.querySelector("#input_setlist_search").value);
      $scope.loading = true;
      console.log(search_term);
      $http.post('/setlistSearch', search_term)
      .then(function successCallback(response) ***REMOVED***
        $scope.loading = false;
        $scope.tracks = response.data;
        if ($scope.page === "even" || $scope.page === 0) ***REMOVED***
          $scope.page = "odd";
        ***REMOVED*** else ***REMOVED***
          $scope.page = "even";
        ***REMOVED***
      ***REMOVED***, function errorCallback(response) ***REMOVED***
          console.log("Error\n" + response);
      ***REMOVED***);
    ***REMOVED***;
  ***REMOVED***);
