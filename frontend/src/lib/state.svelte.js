/**
 * The file contains the client-side state object that
 * is updated whenever new state is retrieved from the
 * backend.
 * 
 * For now, we just return some example state. Eventually
 * this will be retrieved from the backend.
 */
const example_state = {
	state: {
		attributes: {},
		nodes: [
			{
				key: '1',
				attributes: {
					label: 'Node 1',
					x: 0,
					y: 0,
					size: 10,
					color: 'blue'
				}
			},
			{
				key: '2',
				attributes: {
					label: 'Node 2',
					x: 1,
					y: 1,
					size: 20,
					color: 'red'
				}
			}
		],
		edges: [
			{
				key: 'geid_192_0',
				source: '1',
				target: '2',
				attributes: {
					size: 5,
					color: 'purple'
				}
			}
		]
	}
}

export const data = $state(example_state);