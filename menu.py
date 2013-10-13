import os

ans=True

while ans:
	print("""
	1. Limbo
	2. Lust
	3. Gluttony
	4. Greed
	5. Anger
	6. Heresy
	7. Violence
	8. Fraud
	9. Treachery
	0. Quit
	""")
	ans=input("Which level would you like to play? ")
	if ans == 1:
		print("\nopen limbo.py")
		os.system("python2 limbo.py")
	elif ans == 4:
		print("\nopen greed.py")
		os.system("python2 greed.py")
	elif ans == 7:
		print("\nopen violence.py")
		os.system("python2 violence.py")
	elif ans == 0:
		print("\nExiting now")
		break
	elif ans != "":
		print("\nPlease buy our new DLCs")
