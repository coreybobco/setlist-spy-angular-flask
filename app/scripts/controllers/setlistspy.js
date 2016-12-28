'use strict';

/**
 * @ngdoc function
 * @name setlistspyApp.controller:SetlistSpyCtrl
 * @description
 * # SEtlistSpyCtrl
 * Controller of the setlistspyApp
 */
angular.module('setlistspyApp')
  .controller('SetlistSpyCtrl', function ($scope, $http) {
    $scope.tracks = [];
    $scope.page = 0;
    $scope.image = "images/setlistspy_logo.jpg";
    $scope.loading = false;
    $scope.data = {
      selectedIndex: 0
    }
    $scope.setlistSearch = function() {
      var search_term = JSON.stringify(document.querySelector("#input_setlist_search").value);
      $scope.loading = true;
      $scope.error = false;
      $http.post('/setlistSearch', search_term)
      .then(function successCallback(response) {
        $scope.loading = false;
        var results = response.data;
        // $scope.dj_tracks = results['dj_tracks'];
        $scope.DJgridOptions = { data: results['dj_tracks'],
                                 enableFiltering: true,
                                 columnDefs: [{field: 'track', displayName: 'Artist - Track', width: 360, cellTemplate: '<div class="ui-grid-cell-contents">{{row.entity.artist}} - {{row.entity.title}}</div>'},
                                              { field: 'label', displayName: 'Label', width: 190 }]
                         };
        $scope.djs_by_setlist = results['djs_by_setlist'];
        $scope.ArtistgridOptions = { data: results['artist_tracks'],
                                     enableFiltering: true,
                                     columnDefs: [{ field: 'track', displayName: 'Track Title', width: 240},
                                                  { field: 'setlist_urls', displayName: 'Setlists', width: 400, cellTemplate: '<div class="ui-grid-cell-contents"><ul><li ng-repeat="url in row.entity.setlist_urls"><a target="_blank" href="{{url}}">{{grid.appScope.djs_by_setlist[url]}} </a></li></ul></div>'}]};
        if ($scope.page === "even" || $scope.page === 0) {
          $scope.page = "odd";
        } else {
          $scope.page = "even";
        }
      }, function errorCallback(response) {
          $scope.loading = false;
          $scope.error = true;
          console.log("Error\n" + response);
      });
    };
  });
