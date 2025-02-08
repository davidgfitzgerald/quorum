/**
 * The `graphData` object contains the client-side object 
 * that represents the live state of the graph. It is updated 
 * whenever new state is retrieved from the backend.
 */
export const graphData = $state({ state: {} });

/**
 * The `web` object contains the stateful client-side 
 * WebSocket that connects to the backend. It is `websocket.js`
 * that manages the lifecycle of this object. 
 * 
 * Unforunately, svelte 5 pigeonholes us into defining multi-file 
 * state in an object like this. This API means that the socket 
 * is accessed via `web.socket` instead of simply `websocket`.
 * 
 * See here: https://dev.to/mandrasch/svelte-5-share-state-between-components-for-dummies-4gd2
 */
export const web = $state({ socket: null });
