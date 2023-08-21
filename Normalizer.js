let harf = '0-9٠-٩\u0620-\u064A\u066E-\u06D5\u06FA-\u06FF\u0750-\u077F'; //\u08A0-u08FF
let haraka = '\u064B-\u065F';

function wordCount(text) {
	let t = text.match(new RegExp('[' + harf + haraka + ']+', 'g'));
	return (t) ? t.length : 0;
}

function replaceByArray(text, array) {
	if (text) {
		for (let i = 0; i < array.length; i += 2)
			text = text.replace(new RegExp(array[i], 'gim'), array[i + 1]);
	}
	return text;
}

var AliK = [
	'لاَ|لآ|لاً', 'ڵا',
	'لً|لَ|لأ', 'ڵ',
	'ة', 'ە',
	'ه' + '([^ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنوۆەهھیێأإآثذصضطظكيىةڎۊؤ]|$)', 'هـ$1',
	'ض', 'چ',
	'ث', 'پ',
	'ظ', 'ڤ',
	'ط', 'گ',
	'ك', 'ک',
	'ىَ|يَ|یَ|آ', 'ێ',
	'رِ', 'ڕ',
	'ؤ|وَ', 'ۆ',
	'ي|ى', 'ی',
	'ء', '\u200Cو',
	'ِ', '',
	'ذ', 'ژ',
];

var AliWeb = [
	'لاَ|لآ|لاً', 'ڵا',
	'لَ|پ', 'ڵ',
	'ة', 'ە',
	'ه', 'ھ',
	'ه', 'ھ',
	'رِ|أ', 'ڕ',
	'ؤ|وَ', 'ۆ',
	'يَ|یَ', 'ێ',
	'ص', 'ێ',
	'ي', 'ی',
	'ط', 'ڭ',
	'گ', 'ط',
	'ڭ', 'گ',
	'ض', 'چ',
	'ث', 'پ',
	'ظ', 'ڤ',
	'ْ|ُ', '',
	'ى', '*',
	'ك', 'ک',
	'ذ', 'ژ'
];

var Dylan = [
	'لإ|لأ|لآ', 'ڵا',
	'ؤ|وَ', 'ۆ',
	'ة', 'ە',
	'ض', 'ڤ',
	'ص', 'ڵ',
	'ث', 'ێ',
	'ؤ', 'ۆ',
	'ه', 'ھ',
	'ك', 'ک',
	'ي|ى', 'ی',
	'ذ', 'ڕ'
];

var ClearFormatting1 = [
	'<!--(.*?)-->', '', // comment
	'[\r]+', '',
	'[\n]+', ' ',
	'(\\S)  (\\S)', '$1 $2',
	'&nbsp;', ' ',
	'<img .+?>', '',
	'</?o:p>', '', //copy from MS Word
	'<v:shapetype.*?>.*?<\/v:shapetype>', '', //copy from MS Word
	'<v:shape.*?>.*?<\/v:shape>', '', //copy from MS Word
	'<hr.*?>', '',
	'<a.+?>(.*?)<\/a>', '$1',
	'<span[^>]*?>\\s*</\span>', '',
	'<\/b>\\s*<b>', ''
];
var ClearFormatting2 = [
	'<([a-zA-Z1-9]+) .*?>', '<$1>',
	'<span id="menu".*?>([^<]*?)<\/span>', '',
	'\u200C{2,}', '‌', //zwnj
	'<\/?pre.*?>', '‌',
	'<span.*?>', '',
	'<\/span>', '',
	'<(p|h\\d)>', '<div>',
	'<\/(p|h\\d)>', '</div>'
];

function clearFormatting(text) {
	text = replaceByArray(text, ClearFormatting1);
	text = text.replace(/<span[^>]+?font-family:[^>]*Ali_K_.+?>(.+?)<\/span>/gm, function (match, capture) {
		return replaceByArray(capture, AliK);
	});
	text = text.replace(/<span[^>]+?font-family:[^>]*Ali_Web_.+?>(.+?)<\/span>/gm, function (match, capture) {
		return replaceByArray(capture, AliWeb);
	});
	text = text.replace(/<span[^>]+?font-family:[^>]*Dylan.+?>(.+?)<\/span>/gm, function (match, capture) {
		return replaceByArray(capture, Dylan);
	});
	text = replaceByArray(text, ClearFormatting2).trim();
	text = NormalizeUnicode(text);
	text = InitialsFix(text);
	return text;
}

function InitialsFix(text) {
	//رەش←ڕەش  وورچ←ورچ
	text = text.replace(new RegExp(`(^|[^${harf}${haraka}])ر([${harf}${haraka}])`, 'g'), '$1ڕ$2');
	text = text.replace(new RegExp(`(^|[^${harf}${haraka}])وو([${harf}${haraka}])`, 'g'), '$1و$2');
	return text;
}


var CorrectionsNormalize = [
	'ي|ى|ے', 'ی',
	'یٔ', 'ئ',
	'ك|ڪ', 'ک',
	'[رڕ][ٍِ]', 'ڕ',
	'[ٍِ][رڕ]', 'ڕ',
	'[ًٌَُ][ی]', 'ێ',
	'[ی][ًٌَُ]', 'ێ',
	'[ًٌَُ][ڵل]', 'ڵ',
	'[ڵل][ًٌَُ]', 'ڵ',
	'[ًٌَُ][وۆؤ]', 'ۆ',
	'[وۆؤ][ًٌَُ]', 'ۆ',
	'\u200C{2,}', '\u200c',
	'\u06BE([^ـ' + harf + haraka + ']|$)', 'هـ$1',
	'\u06BE', 'ه',
	'\u0647\u200C', '\u06D5',
	'\u0647\u200D', 'هـ',
	'([ءادرڕزژوۆە])\u200C', '$1',
	'\u0647([^ـ' + harf + haraka + ']|$)', '\u06D5$1',
	'\u200Cو ', ' و ',
	'\u200C([^' + harf + ']|$)', '$1',
	'(^|[^' + harf + '])\u200C', '$1',
	'ـ{2,}', 'ـ',
	'ـ' + '([ئبپتجچحخسشعغفڤقکگلڵمنهیێءادرڕزژۆە])', '$1',
	'([بپتجچحخسشعغفڤقکگلڵمنیێ])' + 'ـ', '$1',
	'(^|[^هئ])' + 'ـ', '$1-'
];

function NormalizeUnicode(text) {
	return replaceByArray(text, CorrectionsNormalize);
}

let p1 = '[:؛؟!،,،]';
let p2 = '[«\\(\\[]';
let p3 = 'ی|یش|ش|ان|ەم|هەم|ەمین|هەمین|مان|تان|ەکە|ێک';
let p4 = '[^ <>\\d\n\r"]';
let p5 = '[\\)\\]»]';
let regex_P = new RegExp('(' +
	'[\u003F,;"\u201C\u201D‐―–‒]|' +
	'\\(\\(|' +
	' *\\)\\)|' +
	'»[^\\)<>ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنوۆەهھیێ :؛؟!،.،,]|' +
	' \\.|' +
	` *${p1}${p4}|` +
	` +${p1}${p4}?|` +
	`${p4}${p2} *|` +
	`${p4}?${p2} |` +
	`\\d (${p3}) |` +
	` +${p5}|` +
	' {3,}' +
	')', 'g');

function NormalizePunctuations(text) {
	let Corrections = [		
		'[‐―–‒]', '-', //  -  ‐  ‑  ― – — ‒ _
		'(\u201C|\\(\\()', '«', // “ ((
		'(\u201D|\\)\\))', '»', // ” ))
		'([\\w' + harf + '])( +)([،:؛؟!)}\\]»])( *)', '$1$3 ', // A )
		'([،:؛؟!)}\\]»])' + '([\\S])', '$1 $2', // )A
		'([،:؛؟!)}\\]»])' + ' ([.،:؛؟!)}\\]»])', '$1$2', // ) ,
		'\\.([' + harf + ']{2,})', '. $1', // .AB
		'([' + harf + ']) \\.', '$1.', // AB .
		'([«\\[({])( +)(\\S+)', '$1$3', // ( A
		'(\\S+)([«\\[({])', '$1 $2', // A(
	];
	return replaceByArray(text, Corrections);
};