from typing import List
import itertools


class SudokuHelper:

	@staticmethod
	def thermo(start: int, end: int, length: int) -> List[List[int]]:
		if start > end:
			return []	
		dof = (end - start) - length + 1
		if dof < 0:
			return []

		allvalues = range(1, 10)
		output = []
		for i in range(length):
			output.append(list(allvalues[i:i+dof+1]))
		return output
	
	@staticmethod
	def killer_cage(
		cell_count: int,
		cage_total: int,
		must_include: List[int] = [],
		must_not_include: List[int] = []
		) -> List[List[int]]:

		allvalues = range(1, 10)

		# Make sure that solutions are possible!
		min_possible = sum(allvalues[:cell_count])
		max_possible = sum(allvalues[-cell_count:])
		if not min_possible <= cage_total <= max_possible:
			return []

		# Use dynamic programming pattern to create candidate outputs
		outputs = [[x] for x in allvalues]

		for i in range(cell_count-1):
			new_output = []
			for solution in outputs:
				for value in allvalues:
					new_solution = solution.copy()
					# test various conditions for stopping
					if value in new_solution:
						# each value can only appear once in a cage
						continue
					elif sum(new_solution) + value > cage_total:
						# invalid if sum exceeds cage total
						continue
					else:
						new_solution.append(value)
						new_output.append(new_solution)
			outputs = new_output.copy()

		final_outputs = [sorted(x) for x in new_output if sum(x) == cage_total]
		final_outputs.sort()
		final_outputs = list(final_outputs for final_outputs,_ in itertools.groupby(final_outputs))

		remove based on optional conditions
		if must_include:
			for value in must_include:
				final_outputs = [x for x in final_outputs if value in x]

		if must_not_include:
			for value in must_not_include:
				final_outputs = [x for x in final_outputs if value not in x]

		return final_outputs
		
		
if __name__=="__main__":
	s = SudokuHelper()
	# print(s.thermo(start=1, end=7, length=5))
	print(s.killer_cage(cell_count=7, cage_total=42))
