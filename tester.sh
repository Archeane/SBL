#!/bin/bash
cc=0
wrong_cases=()
for (( i=1 ; i<=50 ; i++ ))
do
	# echo ""
	# echo "***TEST CASE $i***"
	# echo "Input Program:"
	# cat tests/input_$i.txt
	expected_output=$(cat tests/output_$i.txt)
	actual_output=$(python3 aparser.py tests/input_$i.txt)
	

	if [[ "$expected_output" == "$actual_output" ]]; then
		((cc++))
	elif [[ "$expected_output" != "$actual_output" ]]; then
		wrong_cases+=( $i )
		# printf "\nEXPECTED OUTPUT:\n"
		# echo "${expected_output}"
		# printf "ACTUAL OUTPUT:\n"
		# echo "${actual_output}"
	fi
done
echo "$cc / 50 correct"
echo "Incorrect Cases: "
for c in "${wrong_cases[@]}"; do
	echo "$c"
done