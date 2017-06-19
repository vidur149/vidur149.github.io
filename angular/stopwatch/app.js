angular.module('counter', [])
    .controller("myCtrl", ['$scope', '$window', '$interval', function($scope, $window, $interval) {

        $scope.state = 'reset';

        $scope.time = function() {
            if ($window.localStorage.getItem('watchValue') == null) {
                $window.localStorage.setItem('watchValue', '00:00:00');
            }
            return $window.localStorage.getItem('watchValue');
        };

        $scope.startWatch = function() {
            $scope.state = 'start';
            $scope.watchValue = $scope.time();
            var watchArray = $scope.watchValue.split(':');
            var hours = Number(watchArray[0]);
            var minutes = Number(watchArray[1]);
            var seconds = Number(watchArray[2]);
            $scope.totalSeconds = hours * 3600 + minutes * 60 + seconds;

            if ($scope.myInterval) {
                $interval.cancel($scope.myInterval);
            }

            $scope.onInterval = function() {
                $scope.totalSeconds++;
                var hours = Math.floor($scope.totalSeconds / 3600);
                var minutes = Math.floor(($scope.totalSeconds - (hours * 3600)) / 60);
                var seconds = $scope.totalSeconds - (hours * 3600) - (minutes * 60);

                if (hours < 10) { hours = "0" + hours; }
                if (minutes < 10) { minutes = "0" + minutes; }
                if (seconds < 10) { seconds = "0" + seconds; }
                $scope.watchValue = hours + ':' + minutes + ':' + seconds;
                $window.localStorage.setItem('watchValue', $scope.watchValue);
            };

            $scope.myInterval = $interval($scope.onInterval, 1000);

        };

        $scope.stopWatch = function() {
            $scope.state = 'stop';
            if ($scope.myInterval) {
                $interval.cancel($scope.myInterval);
            }
        };

        $scope.resetWatch = function() {
            $scope.state = 'reset';
            $window.localStorage.setItem('watchValue', '00:00:00');
        }
    }]);