'use strict';

/**
 * @ngdoc function
 * @name markovmutatorApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the markovmutatorApp
 */
angular.module('markovmutatorApp')
  .controller('MainCtrl', function ($scope, $http) ***REMOVED***
    $scope.mutagens = [];
    $scope.addBook = function() ***REMOVED***
      var url = JSON.stringify(document.querySelector("#url").value);
      $http.post('/addBook', url)
      .then(function successCallback(response) ***REMOVED***
        var mutagen = response.data;
        var duplicate_found = false;
        for(var i = 0; i < $scope.mutagens.length; i++) ***REMOVED***
          if (mutagen.source == $scope.mutagens[i].source && mutagen.document_id == $scope.mutagens[i].document_id) ***REMOVED***
            duplicate_found = true;
            break;
          ***REMOVED***
        ***REMOVED***
        if (!duplicate_found) ***REMOVED***
          $scope.mutagens.push(mutagen);
        ***REMOVED***
      ***REMOVED***, function errorCallback(response) ***REMOVED***
        console.log("Error\n" + response)
      ***REMOVED***);
  ***REMOVED***
  ***REMOVED***);
