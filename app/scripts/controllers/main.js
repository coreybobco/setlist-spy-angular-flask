'use strict';

/**
 * @ngdoc function
 * @name markovmutatorApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the markovmutatorApp
 */
angular.module('markovmutatorApp')
  .controller('MainCtrl', function ($scope) ***REMOVED***
    $scope.addBook = function() ***REMOVED***
      var url = JSON.stringify(document.querySelector("#url").value);
      var req = new XMLHttpRequest();
      req.addEventListener("load", console.log);
      req.open("post", "./addBook", true);
      req.send(url);
  ***REMOVED***
  ***REMOVED***);
