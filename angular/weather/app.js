(function() {
    angular.module('counter', ['vsGoogleAutocomplete'])
        .controller("Weather", ['$scope', '$http', function($scope, $http) {
            // get todays date and set the state according to hour of the day
            $scope.date = new Date();
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

                $http.get(weather_endpoint).then(function(response) {
                    $scope.response = response.data;
                    $scope.img_src = "https://openweathermap.org/img/w/" + $scope.response.weather[0].icon + '.png';
                    console.log($scope.response);
                });
            };
        }]);
})();