interface Golfer {
	golfer: string;
	name: string;
	pic: string;
}

const golfers: Golfer[] = [
	{
		golfer: 'rory',
		name: 'Rory McIlroy',
		pic: './rory_mcilroy.png',
	},
	{
		golfer: 'tommy',
		name: 'Tommy Fleetwood',
		pic: './tommy_fleetwood.png',
	},
	{
		golfer: 'jon',
		name: 'Jon Rahm',
		pic: './jon_rahm.png',
	},
	{
		golfer: 'bryson',
		name: 'Bryson DeChambeau',
		pic: './bryson_dechambeau.png',
	},
	{
		golfer: 'justin',
		name: 'Justin Thomas',
		pic: './justin_thomas.png',
	},
	{
		golfer: 'jordan',
		name: 'Jordan Spieth',
		pic: './jordan_spieth.png',
	},
	{
		golfer: 'adam',
		name: 'Adam Scott',
		pic: './adam_scott.png',
	},
	{
		golfer: 'scottie',
		name: 'Scottie Scheffler',
		pic: './scottie_scheffler.png',
	},
	{
		golfer: 'xander',
		name: 'Xander Schauffele',
		pic: './xander_schauffele.png',
	},
	{
		golfer: 'viktor',
		name: 'Viktor Hovland',
		pic: './viktor_hovland.png',
	},
	{
		golfer: 'collin',
		name: 'Collin Morikawa',
		pic: './collin_morikawa.png',
	},
	{
		golfer: 'tiger',
		name: 'Tiger Woods',
		pic: './tiger_woods.png',
	},
	{
		golfer: 'nelly',
		name: 'Nelly Korda',
		pic: './nelly_korda.png',
	},
	{
		golfer: 'lydra',
		name: 'Lydia Ko',
		pic: './lydia_ko.png',
	},
];

export function getFullname(golfer: string): string | undefined {
	const foundGolfer = golfers.find((g) => g.golfer === golfer.toLowerCase());
	return foundGolfer ? foundGolfer.name : undefined;
}

export function getPic(golfer: string): string | undefined {
	const foundGolfer = golfers.find((g) => g.golfer === golfer.toLowerCase());
	return foundGolfer ? foundGolfer.pic : undefined;
}
