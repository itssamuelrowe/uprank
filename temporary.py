numbers = input().split(' ')

numberOfHouses = int(numbers[0])
numberOfCoins = int(numbers[1])

total = 0
for i in range(1, numberOfHouses + 1, 2):
    total += numberOfCoins

print(total)