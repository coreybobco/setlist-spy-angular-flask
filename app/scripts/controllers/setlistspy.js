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
    $scope.data = ***REMOVED***
      selectedIndex: 0
    ***REMOVED***
    $scope.setlistSearch = function() ***REMOVED***
      var search_term = JSON.stringify(document.querySelector("#input_setlist_search").value);
      $scope.loading = true;
      $scope.error = false;
      $http.post('/setlistSearch', search_term)
      .then(function successCallback(response) ***REMOVED***
        $scope.loading = false;
        var results = response.data;
        // $scope.dj_tracks = results['dj_tracks'];
        $scope.DJgridOptions = ***REMOVED*** data: results['dj_tracks'],
                                 enableFiltering: true,
                                 columnDefs: [***REMOVED***field: 'track', displayName: 'Artist - Track', width: 470, cellTemplate: '<div class="ui-grid-cell-contents">***REMOVED******REMOVED***row.entity.artist***REMOVED******REMOVED*** - ***REMOVED******REMOVED***row.entity.title***REMOVED******REMOVED***</div>'***REMOVED***,
                                              ***REMOVED*** field: 'label', displayName: 'Label', width: 190 ***REMOVED***]
                         ***REMOVED***;
        $scope.ArtistgridOptions = ***REMOVED*** data: results['artist_tracks'],
                                     enableFiltering: true,
                                     columnDefs: [***REMOVED*** field: 'track', displayName: 'Track Title', width: 240, grouping: ***REMOVED*** groupPriority: 0 ***REMOVED***,
                                                    cellTemplate: '<div ng-if="!col.grouping || col.grouping.groupPriority === undefined || col.grouping.groupPriority === null || ( row.groupHeader && col.grouping.groupPriority === row.treeLevel )" class="ui-grid-cell-contents" title="TOOLTIP">***REMOVED******REMOVED***COL_FIELD CUSTOM_FILTERS***REMOVED******REMOVED***</div>',
                                                    groupHeaderCellTemplate: '<div>***REMOVED******REMOVED***row.entity.title***REMOVED******REMOVED*** [***REMOVED******REMOVED***row.entity.label***REMOVED******REMOVED***]</div>'***REMOVED***,
                                        ***REMOVED*** field: 'dj', displayName: 'DJ', width: 200 ***REMOVED***]***REMOVED***;
        if ($scope.page === "even" || $scope.page === 0) ***REMOVED***
          $scope.page = "odd";
        ***REMOVED*** else ***REMOVED***
          $scope.page = "even";
        ***REMOVED***
      ***REMOVED***, function errorCallback(response) ***REMOVED***
          $scope.loading = false;
          $scope.error = true;
          console.log("Error\n" + response);
      ***REMOVED***);
    ***REMOVED***;
  ***REMOVED***);
