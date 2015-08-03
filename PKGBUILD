# Maintainer: Chris Warrick <aur@chriswarrick.com>
pkgname=cheqlist
_pyname=cheqlist
pkgver=0.1.0
pkgrel=1
pkgdesc='A simple Qt checklist.'
arch=('any')
url='https://github.com/Kwpolska/cheqlist'
license=('BSD')
depends=('python' 'python-setuptools' 'python-pyqt5')
options=(!emptydirs)
source=("https://pypi.python.org/packages/source/${_pyname:0:1}/${_pyname}/${_pyname}-${pkgver}.tar.gz")
md5sums=('4828e8b4cefd1b3494e3eba5aed79b8d')

package() {
  cd "${srcdir}/${_pyname}-${pkgver}"
  python3 setup.py install --root="${pkgdir}/" --optimize=1
  install -D -m644 LICENSE "${pkgdir}/usr/share/licenses/${pkgbase}/LICENSE"
}

# vim:set ts=2 sw=2 et:
