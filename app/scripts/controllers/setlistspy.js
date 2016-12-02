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
    $scope.genes = [];
    $scope.setlistSearch = function(url) ***REMOVED***
      var url = (url) ? JSON.stringify(url) : JSON.stringify(document.querySelector("#url").value);
      $http.post('/setlistSearch', url)
      .then(function successCallback(response) ***REMOVED***
        // document.querySelector("#mutate_button").disabled = false;
        // var gene = response.data;
        // var duplicate_found = false;
        // for(var i = 0; i < $scope.genes.length; i++) ***REMOVED***
        //   if (gene.source == $scope.genes[i].source && gene.document_id == $scope.genes[i].document_id) ***REMOVED***
        //     duplicate_found = true;
        //     break;
        //   ***REMOVED***
        // ***REMOVED***
        // if (!duplicate_found) ***REMOVED***
        //   $scope.genes.push(gene);
        // ***REMOVED***
      ***REMOVED***, function errorCallback(response) ***REMOVED***
        console.log("Error\n" + response)
      ***REMOVED***);
    ***REMOVED***;
  ***REMOVED***);
