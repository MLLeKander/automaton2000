# Maintainer: Michishige Kaito <me@mkaito.com>
_pkgname=Automaton2000
pkgname=python-automaton2000
pkgver=0.1
pkgrel=1
pkgdesc="A simple IRC bot written in Python"
arch=(any)
url="http://www.github.com/mkaito/automaton2000"
license=('GPL')
depends=('python' 'python-yaml' 'python-distribute')
provides=('automaton2000')
backup=('etc/automaton2000/config.yml')
install='automaton2000.install'
source=('Automaton2000-0.1.tar.gz', 'automaton2000')
md5sums=()

package() {
  cd "$srcdir/$_pkgname-$pkgver"
  python3 setup.py install --root="$pkgdir/" --optimize=1
  install automaton2000 /etc/rc.d
}

# vim:set ts=2 sw=2 et:
