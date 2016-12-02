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
    $scope.setlistSearch = function(search_term) ***REMOVED***
      console.log(search_term);
      var search_term = (search_term) ? JSON.stringify(search_term) : JSON.stringify(document.querySelector("#input_setlist_search").value);
      console.log(search_term);
      $http.post('/setlistSearch', search_term)
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
