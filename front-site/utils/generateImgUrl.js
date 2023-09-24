export default class GenerateImgUrl {
  constructor (nmId, photoSize, photoNumber) {
    if (typeof nmId !== 'number' || nmId < 0) {
      throw new Error('Invalid nmId value')
    }
    this.nmId = parseInt(nmId, 10)
    this.size = photoSize || 'c246x328'
    this.number = photoNumber || 1
  }

  getHost (id) {
    if (id >= 0 && id <= 143) {
      return '//basket-01.wb.ru'
    } else if (id >= 144 && id <= 287) {
      return '//basket-02.wb.ru'
    } else if (id >= 288 && id <= 431) {
      return '//basket-03.wb.ru'
    } else if (id >= 432 && id <= 719) {
      return '//basket-04.wb.ru'
    } else if (id >= 720 && id <= 1007) {
      return '//basket-05.wb.ru'
    } else if (id >= 1008 && id <= 1061) {
      return '//basket-06.wb.ru'
    } else if (id >= 1062 && id <= 1115) {
      return '//basket-07.wb.ru'
    } else if (id >= 1116 && id <= 1169) {
      return '//basket-08.wb.ru'
    } else if (id >= 1170 && id <= 1313) {
      return '//basket-09.wb.ru'
    } else if (id >= 1314 && id <= 1601) {
      return '//basket-10.wb.ru'
    } else if (id >= 1602 && id <= 1655) {
      return '//basket-11.wb.ru'
    } else {
      return '//basket-12.wb.ru'
    }
  }

  url () {
    const vol = ~~(this.nmId / 1e5)
    const part = ~~(this.nmId / 1e3)

    return `https:${this.getHost(vol)}/vol${vol}/part${part}/${
      this.nmId
    }/images/${this.size}/${this.number}.jpg`
  }
}
