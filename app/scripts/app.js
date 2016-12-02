'use strict';

/**
 * @ngdoc overview
 * @name markovmutatorApp
 * @description
 * # markovmutatorApp
 *
 * Main module of the application.
 */
var myApp = angular
  .module('markovmutatorApp', [
    'ngAnimate',
    'ngMessages',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'thatisuday.ng-image-gallery'
  ])
  .config(function ($routeProvider) ***REMOVED***
    $routeProvider
      .when('/', ***REMOVED***
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about',
        activetab: 'about'
      ***REMOVED***)
      .when('/mutagen', ***REMOVED***
        templateUrl: 'views/mutagen/index.html',
        controller: 'MutagenCtrl',
        controllerAs: 'mutagen'
      ***REMOVED***)
      .when('/collagenerator', ***REMOVED***
        templateUrl: 'views/collagenerator.html',
        controller: 'CollageneratorCtrl',
        controllerAs: 'collagenerator'
      ***REMOVED***)
      .when('/setlistspy', ***REMOVED***
        templateUrl: 'views/setlistspy.html',
        controller: 'SetlistSpyCtrl',
        controllerAs: 'setlistspy'
      ***REMOVED***)
      .when('/art', ***REMOVED***
        templateUrl: 'views/art.html',
        controller: 'ImageCtrl',
        controllerAs: 'art',
        activetab: 'art'
      ***REMOVED***)
      .when('/writings', ***REMOVED***
        templateUrl: 'views/writings.html',
        controller: 'WritingCtrl',
        controllerAs: 'writimgs',
        activetab: 'writings'
      ***REMOVED***)
      .otherwise(***REMOVED***
        redirectTo: '/'
      ***REMOVED***);
  ***REMOVED***).controller('HeaderCtrl', function HeaderController($scope, $location)
  ***REMOVED***
    $scope.isActive = function (viewLocation) ***REMOVED***
      return viewLocation === $location.path();
    ***REMOVED***;
  ***REMOVED***);

myApp.filter('range', function() ***REMOVED***
  return function(input, total) ***REMOVED***
    total = parseInt(total);

    for (var i=0; i<total; i++) ***REMOVED***
      input.push(i);
    ***REMOVED***

    return input;
  ***REMOVED***;
***REMOVED***);
