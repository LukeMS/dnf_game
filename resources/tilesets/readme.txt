pattern =
	_tile####$theme$##px$##v$description.png:
		_tile####: #### is the id of the tile (e.g. _id0046 for the floor);
		theme: if the tile is to be used in a specific level theme or is "default";
		##px: size, in pixels (e.g. 32px);
		##v: number of tile variations (on map draw it will be randomized up to this number);
		description: for easier reference, not used by the game.
		