from rest_framework import serializers
from market_app.models import Market, Seller, Product


class MarketSerializer(serializers.HyperlinkedModelSerializer):
    sellers = serializers.HyperlinkedRelatedField(many =True, read_only = True, view_name = 'seller-detail')
    class Meta:
        model = Market
        fields = ['id', 'name', 'description', 'net_worth','sellers']
        read_only_fields = ['id']

class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many = True, read_only= True)
    market_ids = serializers.PrimaryKeyRelatedField(
        queryset = Market.objects.all(),
        many= True,
        write_only = True,
        source = 'markets'
    )
    
    market_count = serializers.SerializerMethodField()
    
    class Meta:
        model= Seller
        fields = ['id', 'name', 'contact_info','markets', 'market_ids','market_count' ]
    
    def get_market_count(self, obj):
        return obj.markets.count()

class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only= True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    # markets = MarketSerializer(read_only = True, many =True)
    markets = serializers.StringRelatedField(many = True)
         
class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child = serializers.IntegerField(),write_only = True)
    
    def validate_markets(self, value):
        markets = Market.objects.filter(id__in = value)
        if len(markets) != len(value):
            raise serializers.ValidationError("One or More Market Ids not Found")
        return value
    
    def create(self, validated_data):
        market_ids = validated_data.pop("markets")
        seller = Seller.objects.create(**validated_data)
        markets = Market.objects.filter(id__in = market_ids)
        seller.markets.set(markets)
        return seller

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def validate(self, data):
        market = data["market"]
        seller = data["seller"]
        if not seller.markets.filter(id=market.id).exists():
            raise serializers.ValidationError(
                "This seller is not associated with the selected market."
            )
        return data
 
class ProductDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only= True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.StringRelatedField(read_only = True)
    seller = serializers.StringRelatedField(read_only = True)

class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.PrimaryKeyRelatedField(queryset = Market.objects.all())
    seller = serializers.PrimaryKeyRelatedField(queryset = Seller.objects.all())
    
    def validate(self, data):
        market = data["market"]
        seller = data["seller"]
        if not seller.markets.filter(id=market.id).exists():
            raise serializers.ValidationError(
                "This seller is not associated with the selected market."
            )
        return data

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    


