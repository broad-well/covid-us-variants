import Papa from 'papaparse';

const DATA_URL = 'https://raw.githubusercontent.com/broad-well/covid-variants-us-states/main/us-states.csv';

export type DataRow = any; // TODO

export const kAllVariants = {
    b117: 'B.1.1.7',
    p1: 'P.1',
    b1351: 'B.1.351'
} as const;

export async function read() {
    const {data, errors} = Papa.parse(await (await fetch(DATA_URL)).text(), {
        header: true,
        skipEmptyLines: true
    });
    if (errors.length > 0) {
        throw new Error(JSON.stringify(errors[0]));
    }
    return data.map((row: any) => ({
        ...row,
        b117: parseInt(row.b117),
        p1: parseInt(row.p1),
        b1351: parseInt(row.b1351)
    }));
}

export function allStates(rows: DataRow[]) {
    return Array.from(new Set(rows.map(it => it.state))).sort();
}