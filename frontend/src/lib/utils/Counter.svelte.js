export function createCounter() {
	let count = $state(0);

	return {
		get count() { return count },
		next: () => count += 1
	};
}
