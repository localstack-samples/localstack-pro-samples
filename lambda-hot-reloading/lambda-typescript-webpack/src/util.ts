type StringMap<T> = {
  readonly [k: string]: T[keyof T];
};

export function downcaseKeys<T extends Record<string, any>>(o: T): StringMap<T> {
  return Object.keys(o).reduce<StringMap<T>>((no, k) => {
    return { ...no, [k.toLowerCase()]: o[k as keyof T] };
  }, {});
}
