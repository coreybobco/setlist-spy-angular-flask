'use strict';

/**
 * @ngdoc function
 * @name markovmutatorApp.controller:SetlistSpyCtrl
 * @description
 * # SEtlistSpyCtrl
 * Controller of the markovmutatorApp
 */
angular.module('markovmutatorApp')
  .controller('SetlistSpyCtrl', function ($scope, $http) ***REMOVED***
    $scope.tracks = [];
    $scope.page = 0;
    $scope.setlistSearch = function(search_term) ***REMOVED***
      console.log(search_term);
      var search_term = (search_term) ? JSON.stringify(search_term) : JSON.stringify(document.querySelector("#input_setlist_search").value);
      console.log(search_term);
      $http.post('/setlistSearch', search_term)
      .then(function successCallback(response) ***REMOVED***
        console.log("done");
        $scope.tracks = response.data;
        if ($scope.page == "even" || $scope.page == 0) ***REMOVED***
          $scope.page = "odd";
        ***REMOVED*** else ***REMOVED***
          $scope.page = "even";
        ***REMOVED***

      ***REMOVED***, function errorCallback(response) ***REMOVED***
        console.log("Error\n" + response)
      ***REMOVED***);
    ***REMOVED***;
  ***REMOVED***);
