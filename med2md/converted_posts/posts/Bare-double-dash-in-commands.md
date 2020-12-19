---
kicker: -

title: Bare double dash in commands

subtitle: We usually have to use commands for performing various tasks in our daily life as a programmer. Usually every commands have some arguments…

---

We usually have to use commands for performing various tasks in our daily life as a programmer. Usually every commands have some arguments or flags.

![](https://cdn-images-1.medium.com/max/800/0*2nzH2_6m7y8HR6kZ)A single hyphen can be followed by multiple single-character flags. A double hyphen prefixes a single, multicharacter option.

Consider this example:

tar -czfIn this example, -czf specifies three single-character flags: c, z, and f. So -c -z -f is same as -czf .

Now consider another example:

tar --excludeIn this case, --exclude specifies a single, multicharacter option named exclude. The double hyphen disambiguates the command-line argument, ensuring that tar interprets it as exclude rather than a combination of e, x, c, l, u, d, and e.

### But what about bare double dashes??

It is actually part of the POSIX standard that — can be used to separate options from other arguments, so you will see it on commands like cp and mv (which are not part of Bash).

The double dash “–” means end of command line flags i.e. it tells the preceding command not to try to parse what comes after command line options.

If you want to grep a file for the string -v ; normally -v would be considered as the option to reverse the matching meaning (only show lines that do not match), but with — you can grep for string -v like this:

grep -- -v fileA double dash ( — ) is used in bash built-in commands and there are more other commands to signify the end of command options, after which only positional parameters are accepted.


