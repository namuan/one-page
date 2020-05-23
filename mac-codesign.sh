echo "###### OnePage Code Signing ###############"

ID="$1"

for filename in $(find dist/OnePage.app/ -name "*.dylib"); do
    codesign -v -f -s "$ID" $filename
done
for filename in $(find dist/OnePage.app/ -name "*.so"); do
    codesign -v -f -s "$ID" $filename
done

for filename in $(find dist/OnePage.app/Contents/MacOS -name "Qt*"); do
    codesign -v -f -s "$ID" $filename
done

for filename in $(ls dist/OnePage.app/Contents/MacOS/PyQt5/Qt/translations/*); do
    codesign -v -f -s "$ID" $filename
done

codesign -v -f -s "$ID" /Users/nmn/workspace/one-page/dist/OnePage.app/Contents/MacOS/base_library.zip

codesign -v -f --entitlements entitlements.plist -s "$ID" dist/OnePage.app/Contents/MacOS/python
codesign -v -f --entitlements entitlements.plist -s "$ID" dist/OnePage.app/Contents/MacOS/app
codesign -v -f --entitlements entitlements.plist -s "$ID" dist/OnePage.app

# Add verification
# spctl --raw -vvv --assess --type exec dist/OnePage.app