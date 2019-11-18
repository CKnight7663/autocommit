#Constants
K = 1.38E-23
C = 3E8


#Functions
Ray_Jean = lambda{|nu, temp| ((8 * Math::PI * (nu**2) * K * temp)/C**3) }
puts 'Please Input a Frequency: '
user_nu = eval gets
puts 'Please Input a Temperature: '
user_temp = eval gets
puts Ray_Jean.call(user_nu, user_temp)
