angular.module('counter', [])
    .controller("Stopwatch", ['$scope', '$window', '$interval', function($scope, $window, $interval) {

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
            // Watch value is stored in hh:mm:ss format, 
            // hence we need to split it around ':' and then convert into hours,minutes and seconds
            var watchArray = $scope.watchValue.split(':');
            var hours = Number(watchArray[0]);
            var minutes = Number(watchArray[1]);
            var seconds = Number(watchArray[2]);
            // We have to increment the timer value every second, 
            // therefore we need to calculate the total seconds and then only we can 
            // increment the value by 1
            $scope.totalSeconds = hours * 3600 + minutes * 60 + seconds;

            if ($scope.myInterval) {
                $interval.cancel($scope.myInterval);
            }

            $scope.onInterval = function() {
                $scope.totalSeconds++;
                // after incrementing the value we need to convert it back into hh:mm:ss format                
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
            $scope.stopWatch();
            $scope.state = 'reset';
            // console.log($http.jsonp("http://ipinfo.io/json"));
            $window.localStorage.setItem('watchValue', '00:00:00');
        }
    }]);

angular.module('counter')
    .controller("Weather", ['$scope', '$http', function($scope, $http) {

        // get todays date and set the state according to hour of the day
        $scope.date = new Date();
        console.log($scope.date.getHours());
        var hrs = $scope.date.getHours();
        // var hrs = $scope.data.getHours();
        var state = '';
        if (hrs > 6 && hrs < 20) {
            state = 'morning';
        } else if (hrs >= 20 & hrs <= 6) {
            state = 'night';
        }
        $scope.state = state;
        // get lat and lang of current position
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                $scope.lat = position.coords.latitude;
                $scope.long = position.coords.longitude;
                // get weather details of the current lat and long
                $scope.getWeather($scope.lat, $scope.long);
            });
        }

        $scope.getWeather = function(lat, long) {
            var api_key = '&appid=c745ee805737efda1aecd6d7545d8fe0&units=metric';
            var weather_endpoint = 'http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + long + api_key;

            $http.jsonp(weather_endpoint).then(function(response) {
                $scope.response = response.data;
                $scope.img_src = "https://openweathermap.org/img/w/" + $scope.response.weather[0].icon + '.png';
                console.log($scope.response);
            });
        };
    }]);